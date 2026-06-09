import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"

export async function generateMetadata() {

  return {
    title: "Transaction | Summary"
  }
}

/**
 * 
 * @param {string} authToken 
 * @param {string} searchParams 
 * @returns {Promise<{data:object |null , err:null | Array, success:boolean}>}
 */
async function fetchTransactionSummary(authToken, searchParams) {
  const url = "transaction/interpret?" + searchParams

  const res = await sendRequest(url, { providedAuthToken: authToken })

  return res
}


async function page({ searchParams }) {

  // initializing cookie
  const store = await cookies()
  const cookieMgt = CookieManager("server", store)

  // getting the auth token
  const authToken = cookieMgt.getCookie()

  // configuring url params
  const params = new URLSearchParams(await searchParams)

  const res = await fetchTransactionSummary(authToken, params.toString())


  return (
    <div className="flex-auto flex flex-col px-1">
      {!res.success ? <h2 className="self-center mx-auto"> {res.err[0]}  </h2> : <>
        {/* User Summary */}
        <UserSummary data={res?.data?.msg?.user} />


        {/* Location Summary */}

        <section className="my-1">
          <h3 className="text-center poppins-bold">Location Transactions Summary</h3>
          {res?.data?.msg?.location.map((elem, i) => {
            return <p className="my-1 " key={i}> {elem}   </p>
          })}
        </section>
        {/* Comparisons with locationn */}

        <section className="my-2">
          <h3 className="text-center poppins-bold">Geo-Spending Analytics</h3>
          {res?.data?.msg?.comparisons.map((elem, i) => {
            return <p className="" key={i}> {elem}   </p>
          })}
        </section>
      </>}
    </div>
  )
}


function UserSummary({ data }) {

  return <section className="my-2 flex flex-col">
    <h3 className="poppins-bold text-center">User Transactions Summary</h3>

    {/* Amount */}

    <article className="my-1">
      <h5 className="bg-accent-color w-max px-2 mb-1">Amount</h5>
      <p className="">
        {data?.amount}
      </p>
    </article>

    {/* Amount by date */}
    <article className="my-1">
      <h5 className="bg-accent-color w-max px-2 mb-1">Amount By Date</h5>
      {data?.amount_by_date.map((elem, i) => <p className="my-1  " key={i}>{elem}</p>)}
    </article>

    {/* Transaction dates */}
    <article className="my-1">
      <h5 className="bg-accent-color w-max px-2 mb-1">Transaction Dates</h5>
      {data?.transaction_dates.map((elem, i) => <p className="my-1 " key={i}>{elem}</p>)}
    </article>

    {/* Category */}

    <article className="my-1">
      <h5 className="bg-accent-color w-max px-2 mb-1">Category </h5>
      <p className="">
        {data?.category}
      </p>
    </article>

    {/* Flagged */}

    <article className="my-1">
      <h5 className="bg-accent-color w-max px-2 mb-1">Flagged</h5>
      <p className="">
        {data?.flagged}
      </p>
    </article>


    {/* Transaction Type */}

    <article className="my-1">
      <h5 className="bg-accent-color w-max px-2 mb-1">Transaction Type</h5>
      <p className="">
        {data?.transaction_type}
      </p>
    </article>

  </section>

}
export default page