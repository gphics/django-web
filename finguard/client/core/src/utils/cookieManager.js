import { setCookie, getCookie, deleteCookie } from "cookies-next";

/**
 * This class is responsible for performing CRUD operations on the sessions
 */

class BaseClass{
  cookieName = "token"
  getCookie(){}
  deleteCookie(){}
  setCookie(){}
}
class ClientCookieMgt extends BaseClass  {

  cookieOption = {
    maxAge: 60 * 60 * 24 * 30,
    path: "/",
  };

  /**
   * This method get the auth token saved in the cookies
   * @returns string | null
   */
  getCookie() {
    return getCookie(this.cookieName);
  }
  /**
   * This method saves the auth token to the cookie storage
   * @param {string} token
   */
  setCookie(token) {
    setCookie(this.cookieName, token, this.cookieOption);
  }

  /**
   * This method delete the auth token saved in the cookie storage
   */
  deleteCookie() {
    deleteCookie(this.cookieName);
  }
}

class serverCookieMgt extends BaseClass {
  
  constructor(store) {
    super()
    this.cookieStore = store;
  }

  /**
   * This method get the auth token saved in the cookies
   * @returns string | null
   */
  getCookie() {
      const token = this.cookieStore.get(this.cookieName);
      if (!token) return null
      return token.value
  }
  
}


export default function CookieManager(type="client", store=null) {
    if (type === "client") {
        return new ClientCookieMgt()
    } else {
        return new serverCookieMgt(store)
    }
}
