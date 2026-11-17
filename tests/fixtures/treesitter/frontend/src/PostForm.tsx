import axios from "axios";
import { api } from "./api";

/** Saves a post. */
export function handleSave(title: string) {
  return api.posts.create(title);
}

export function PostForm({ id, props }: { id: number; props: any }) {
  const posts = fetch("/api/posts");
  axios.get(`/api/posts`);
  axios.delete(`/api/posts/${id}`);
  function local() {
    return fetch("/hidden");
  }
  return (
    <form>
      <button onClick={handleSave}>{posts.length}</button>
      <Form.Item onChange={() => validate(id)} onBlur={track("blur")} title="t" />
      <input onFocus={props.onFocus} />
    </form>
  );
}
