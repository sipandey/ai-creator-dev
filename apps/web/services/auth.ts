import { apiFetch } from "./api";

export async function getCurrentUser() {
  return apiFetch("/users/me");
}

export async function login(email: string, password: string) {
  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  localStorage.setItem("token", res.access_token);
  return res;
}

export async function signup(
  email: string,
  password: string,
  creator_type: string
) {
  return apiFetch("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ email, password, creator_type }),
  });
}
