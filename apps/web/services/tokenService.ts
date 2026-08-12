import api from "./api";

export async function getTokens() {

  const response =
    await api.get("/tokens");

  return response.data;
}

export async function getToken(
  mint: string
) {

  const response =
    await api.get(`/tokens/${mint}`);

  return response.data;
}