/** A toggle. */
export function useToggle(on: boolean): [boolean, () => void] {
  return [on, () => {}];
}

export type Pair<T> = [T, T];
