import api from "./api";

export async function getWallet(
  wallet: string
) {

  const response =
    await api.get(
      `/wallets/${wallet}`
    );

  return response.data;
}