import api from "./api";

export async function getNarratives() {

  const response =
    await api.get(
      "/narratives"
    );

  return response.data;
}