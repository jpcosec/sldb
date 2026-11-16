import React, { memo } from "react";
import "./app.css";
export { Other } from "./other";

/** Props of a button. */
export interface ButtonProps {
  label: string;
}

/** Not this one. */
/**
 * A button.
 *
 *   Indented.
 */
export function Button({ label }: ButtonProps) {
  function inner() {
    return <span>{label}</span>;
  }
  return inner();
}

/** Counts. */
export const useCounter = (start: number = 0) => {
  const [n, setN] = React.useState(start);
  return { n, inc: () => setN(n + 1) };
};

type Mode = "a" | "b";

/** Gap below, not a doc. */

export const Card = memo(() => <></>);

const helper = x => x * 2;

const NotComponent = () => 1;

export default function () {
  return <Button label="hi" />;
}
