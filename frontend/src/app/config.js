export const config = {
  auth: {
    b2cScopes: [process.env.VUE_APP_AUTH_IMPERSONATION_SCOPE],
    clientId: process.env.VUE_APP_AUTH_CLIENT_ID,
    authorities: {
      signin: process.env.VUE_APP_AUTH_SIGNIN_AUTHORITY,
      passwReset: process.env.VUE_APP_AUTH_PASSW_AUTHORITY,
    },
  },
  api: {
    baseUrl: process.env.VUE_APP_API_URL,
  },
}
