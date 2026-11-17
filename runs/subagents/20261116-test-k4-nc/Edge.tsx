export function useEdge(a: any, xs: string[]) {
  a?.();
  a.b?.();
  a!.c();
  ([] as Array<string>).map(f);
  [1] // comentario
    .map(g);
  'a  b'.split(" ");
  /a  b/.test(x);
  `t  ${a}`.trim();
  (await [y]).at(0);
  new Foo<T>().bar();
  sql`select 1`;
  fetch('/a  b');
  fetch(`/x/${a}`);
  fetch("a\"b");
  a[0].b();
  (function(){})();
  (() => 1)();
  super.x;
  this.y.z();
  import('./m').then(h);
}
export function Comp() {
  return <div>
    <A onClick={() => new Foo().go()} />
    <B onclick={h1} only={h2} on={h3} onX={h4} />
    <C onSubmit={async () => { await save(1); }} />
    <D onChange={e => setV(e.target.value)} />
    <E onClick={function () { run(); }} />
    <F.G onKey={a.b} />
  </div>;
}
