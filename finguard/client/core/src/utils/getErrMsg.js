/**
 * This function helps to decompose the err object and return a list containing the values of the err obj if it is not null
 * @param {object | null} err 
 * @returns {[string] | null}
 */
export default function getErrMsg(err) {
  if (err === null) return null;
  const result = Object.values(err).flatMap((val) => {
    if (typeof val === "object" && val !== null) {
      return getErrMsg(val);
    }
    return val;
  });
    return result
}
