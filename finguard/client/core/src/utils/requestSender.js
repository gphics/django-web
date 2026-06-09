import CookieManager from "./cookieManager";
import getErrMsg from "./getErrMsg";
/**
 * This function send request of all possible method to the server and returns a response.
 * @param {string} url
 * @param {{method:string, isAuth:boolean, body:object, providedAuthToken:null | string, filters: null | object, isRawBody:boolean}} options
 * providedAuthToken is not required to be provided in a client component as this utility function handles it
 * @returns {Promise<{data:null|{msg:string |Array | object}, success:boolean, err:null | [string]}>}
 */
export default async function sendRequest(url, options = {}) {
  try {
    const {
      method = "get",
      isAuth = true,
      body = {},
      providedAuthToken = null,
      filters = null, // useful when filtering transactions
      isRawBody=false
    } = options;
    const cookieMgt = CookieManager();

    // getting | setting the auth token
    const token = providedAuthToken || cookieMgt.getCookie();

    // constructing the server url
    const baseUrl =
      process.env.SERVER_URL || process.env.NEXT_PUBLIC_SERVER_URL;

    // the full url
    let completeUrl = baseUrl + url;

    // adding filters if present
    if (filters) {
      const params = new URLSearchParams(filters);
      completeUrl = completeUrl.includes("?")
        ? `${completeUrl}&${params.toString()}`
        : `${completeUrl}?${params.toString()}`;
    }

    // setting request options
    const reqOptions = {
      method,
      headers: { "Content-Type": "application/json" },
    };

    // adding the body if required
    if (method != "get") {
      reqOptions.body = isRawBody ? body : JSON.stringify(body);
    }

    // adding authenication factors
    if (isAuth) {
      // if not logged in
      if (!token) throw new Error("You are not authenticated");

      // adding auth token
      reqOptions.headers.Authorization = "Token " + token;
    } else {
    }

    // making the request
    const first = await fetch(completeUrl, reqOptions);

    const contentType = first.headers.get("content-type");
    const second =
      contentType && contentType.includes("application/json")
        ? await first.json()
        : { err: "Server returned a non-JSON response" };

    // if an error was returned from the server
    if (second?.err) {
      second.err = getErrMsg(second.err);
    }

    // in case of authentication error returned by default by the server
    if (!second?.err && !second?.data) {
      second.success = false;
      second.err = getErrMsg(second);
    }
    return second;
  } catch (error) {
    return {
      data: null,
      err: getErrMsg({ msg: error?.message || "something went wrong" }),
    };
  }
}
