import { cookies } from "next/headers"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import SingleTransactionComponent from "@/components/TransactionComponent/SingleTransactionComponent"

export async function generateMetadata({ params }) {
    const { id } = await params

    return {
        title: "Transaction| " + id,
        description: "A page containing the full information about transaction " + id
    }
}

async function fetchTransaction(id, authToken) {
    const url = "transaction?id=" + id
    const res = await sendRequest(url, { providedAuthToken: authToken })
    return res
}

async function getUserCurrency(providedAuthToken) {
  const url = "account/profile/currencies?user=yes"
  const res = await sendRequest(url, { providedAuthToken })
  return res
}

async function page({ params }) {

    const { id } = await params

    const store = await cookies()

    const cookieMgt = CookieManager("server", store)

    const authToken = cookieMgt.getCookie()

    const res = await fetchTransaction(id, authToken)

    const currencyRes = await getUserCurrency(authToken)



    return (
        <div className="flex flex-auto px-1 w-full">
            {!res?.success ? <h2 className="self-center mx-auto poppins-bold text-[1.3em] text-rose-500 capitalize"> {res.err[0]} </h2> : <SingleTransactionComponent currencyRes={currencyRes}  data={res?.data?.msg} />}
        </div>
    )
}

export default page