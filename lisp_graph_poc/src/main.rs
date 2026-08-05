use petgraph::graph::{Graph, NodeIndex};
use petgraph::Directed;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::Write;
use std::rc::Rc;
use std::cell::RefCell;

// --- 1. Definición del AST Lisp (EDN / Dialecto Clojure) ---

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Symbol(String),
    Keyword(String), // e.g. :title
    Number(f64),
    String(String),
    List(Vec<Expr>),   // ( ... )
    Vector(Vec<Expr>), // [ ... ]
    Map(Vec<(Expr, Expr)>), // { ... }
    Func(fn(&[Expr], &mut Env) -> Result<Expr, String>),
}

#[derive(Serialize, Deserialize, Debug)]
pub struct AstNodeData {
    pub kind: String,
    pub value: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct AstEdgeData {
    pub relation: String,
}

pub type AstGraph = Graph<AstNodeData, AstEdgeData, Directed>;

// --- 2. Persistencia del AST al Grafo (Structural Mapping) ---

pub fn ast_to_graph(expr: &Expr, graph: &mut AstGraph) -> NodeIndex {
    match expr {
        Expr::Symbol(s) => graph.add_node(AstNodeData { kind: "Symbol".into(), value: s.clone() }),
        Expr::Keyword(k) => graph.add_node(AstNodeData { kind: "Keyword".into(), value: k.clone() }),
        Expr::Number(n) => graph.add_node(AstNodeData { kind: "Number".into(), value: n.to_string() }),
        Expr::String(s) => graph.add_node(AstNodeData { kind: "String".into(), value: s.clone() }),
        Expr::List(list) => {
            let list_node = graph.add_node(AstNodeData { kind: "List".into(), value: format!("List(len={})", list.len()) });
            for (i, item) in list.iter().enumerate() {
                let child_node = ast_to_graph(item, graph);
                graph.add_edge(list_node, child_node, AstEdgeData { relation: format!("child_{}", i) });
            }
            list_node
        }
        Expr::Vector(vec) => {
            let vec_node = graph.add_node(AstNodeData { kind: "Vector".into(), value: format!("Vector(len={})", vec.len()) });
            for (i, item) in vec.iter().enumerate() {
                let child_node = ast_to_graph(item, graph);
                graph.add_edge(vec_node, child_node, AstEdgeData { relation: format!("index_{}", i) });
            }
            vec_node
        }
        Expr::Map(map) => {
            let map_node = graph.add_node(AstNodeData { kind: "Map".into(), value: format!("Map(entries={})", map.len()) });
            for (i, (k, v)) in map.iter().enumerate() {
                let k_node = ast_to_graph(k, graph);
                let v_node = ast_to_graph(v, graph);
                graph.add_edge(map_node, k_node, AstEdgeData { relation: format!("entry_{}_key", i) });
                graph.add_edge(map_node, v_node, AstEdgeData { relation: format!("entry_{}_value", i) });
            }
            map_node
        }
        Expr::Func(_) => graph.add_node(AstNodeData { kind: "NativeFunc".into(), value: "func".into() }),
    }
}

// --- 3. Parsing (EDN / Clojure-like) ---

pub fn tokenize(chars: &mut std::iter::Peekable<std::str::Chars>) -> Vec<String> {
    let mut tokens = Vec::new();
    while let Some(&c) = chars.peek() {
        match c {
            '(' | ')' | '[' | ']' | '{' | '}' => {
                tokens.push(c.to_string());
                chars.next();
            }
            ' ' | '\n' | '\t' | '\r' | ',' => { chars.next(); } // Comas son whitespace en Clojure
            '"' => {
                chars.next();
                let mut s = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch == '"' { chars.next(); break; }
                    s.push(ch);
                    chars.next();
                }
                tokens.push(format!("\"{}\"", s));
            }
            _ => {
                let mut token = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch == '(' || ch == ')' || ch == '[' || ch == ']' || ch == '{' || ch == '}' || ch.is_whitespace() || ch == ',' { break; }
                    token.push(ch);
                    chars.next();
                }
                tokens.push(token);
            }
        }
    }
    tokens
}

pub fn parse(tokens: &mut std::vec::IntoIter<String>) -> Result<Expr, String> {
    let token = tokens.next().ok_or("Unexpected EOF")?;
    match token.as_str() {
        "(" => {
            let mut list = Vec::new();
            while let Some(peek) = tokens.clone().peekable().peek() {
                if peek == ")" { tokens.next(); break; }
                list.push(parse(tokens)?);
            }
            Ok(Expr::List(list))
        }
        "[" => {
            let mut vec = Vec::new();
            while let Some(peek) = tokens.clone().peekable().peek() {
                if peek == "]" { tokens.next(); break; }
                vec.push(parse(tokens)?);
            }
            Ok(Expr::Vector(vec))
        }
        "{" => {
            let mut map = Vec::new();
            while let Some(peek) = tokens.clone().peekable().peek() {
                if peek == "}" { tokens.next(); break; }
                let k = parse(tokens)?;
                let v = parse(tokens)?;
                map.push((k, v));
            }
            Ok(Expr::Map(map))
        }
        ")" | "]" | "}" => Err(format!("Unexpected {}", token)),
        _ => {
            if token.starts_with('"') {
                Ok(Expr::String(token.trim_matches('"').into()))
            } else if token.starts_with(':') {
                Ok(Expr::Keyword(token))
            } else if let Ok(n) = token.parse::<f64>() {
                Ok(Expr::Number(n))
            } else {
                Ok(Expr::Symbol(token))
            }
        }
    }
}

// --- 4. Evaluador Lisp ---

pub struct Env {
    vars: HashMap<String, Expr>,
    outer: Option<Rc<RefCell<Env>>>,
}

impl Env {
    pub fn new() -> Self { Env { vars: HashMap::new(), outer: None } }
    pub fn get(&self, name: &str) -> Option<Expr> {
        if let Some(val) = self.vars.get(name) { Some(val.clone()) } 
        else if let Some(ref outer) = self.outer { outer.borrow().get(name) } 
        else { None }
    }
}

pub fn eval(expr: &Expr, env: &mut Env) -> Result<Expr, String> {
    match expr {
        Expr::Symbol(s) => env.get(s).ok_or_else(|| format!("Unbound symbol: {}", s)),
        Expr::Number(_) | Expr::String(_) | Expr::Keyword(_) | Expr::Func(_) => Ok(expr.clone()),
        Expr::Vector(vec) => {
            let mut ev_vec = Vec::new();
            for item in vec { ev_vec.push(eval(item, env)?); }
            Ok(Expr::Vector(ev_vec))
        }
        Expr::Map(map) => {
            let mut ev_map = Vec::new();
            for (k, v) in map { ev_map.push((eval(k, env)?, eval(v, env)?)); }
            Ok(Expr::Map(ev_map))
        }
        Expr::List(list) => {
            if list.is_empty() { return Ok(expr.clone()); }
            if let Expr::Symbol(ref op) = list[0] {
                match op.as_str() {
                    "def" | "define" => {
                        if let Expr::Symbol(ref name) = list[1] {
                            let val = eval(&list[2], env)?;
                            env.vars.insert(name.clone(), val.clone());
                            return Ok(val);
                        }
                    }
                    "do" | "begin" => {
                        let mut last = Expr::List(vec![]);
                        for exp in &list[1..] { last = eval(exp, env)?; }
                        return Ok(last);
                    }
                    _ => {} // function call
                }
            }
            
            // Eval function call
            let func = eval(&list[0], env)?;
            let mut args = Vec::new();
            for arg in &list[1..] { args.push(eval(arg, env)?); }
            
            if let Expr::Func(f) = func { f(&args, env) } 
            else { Err("Not a function".into()) }
        }
    }
}

fn main() {
    println!("--- Inicializando Kernel EDN / Clojure <-> Grafo Store ---");
    
    // Script EDN/Clojure real, con Mapas, Vectores y Keywords
    let code = r#"
    (do
        (def doc-1 {
            :id "doc-001"
            :title "Arquitectura SLDB"
            :tags [:system :architecture]
        })
        
        doc-1
    )
    "#;
    
    // 1. Parsing a AST EDN
    let mut tokens = tokenize(&mut code.chars().peekable()).into_iter();
    let ast = parse(&mut tokens).unwrap();
    println!("AST Clojure/EDN Parseado Correctamente.");

    // 2. Persistencia en el Grafo
    let mut graph = AstGraph::new();
    let _root = ast_to_graph(&ast, &mut graph);
    
    let serialized = serde_json::to_string_pretty(&graph).unwrap();
    let mut file = File::create("clj_graph_store.json").unwrap();
    file.write_all(serialized.as_bytes()).unwrap();
    println!("-> AST Persistido en 'clj_graph_store.json' ({} nodos).", graph.node_count());

    // 3. Evaluando el AST
    let mut env = Env::new();
    match eval(&ast, &mut env) {
        Ok(result) => println!("-> Resultado Evaluación Lisp/EDN: {:?}", result),
        Err(e) => println!("Error: {}", e),
    }
}
