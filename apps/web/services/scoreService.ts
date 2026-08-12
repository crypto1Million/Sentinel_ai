import api from "./api";

export async function getScore(
  mint: string
) {

  const response =
    await api.get(
      `/scores/${mint}`
    );

  return response.data;
}