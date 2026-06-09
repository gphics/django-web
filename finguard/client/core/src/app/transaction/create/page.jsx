import TransactionCreationComponent from "@/components/TransactionComponent/TransactionCreationComponent"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"


async function fetchCurrency(authToken) {
  const res = await sendRequest("account/profile/currencies?user=yes", { providedAuthToken: authToken })
  return res
}

export async function generateMetadata({ searchParams }) {
  const { id } = await searchParams

  const titleStr = id ? ("Update Transaction |" + id) : "Create Transaction"


  return {
    title: titleStr
  }
}

async function fetchTransaction(transactionId, authToken) {
  const url = "transaction/?id=" + transactionId
  const res = await sendRequest(url, { providedAuthToken: authToken })
  return res
}

async function page({ searchParams }) {

  const { id } = await searchParams

  const store = await cookies()

  const cookieMgt = CookieManager("server", store)

  const authToken = cookieMgt.getCookie()
  const currencyRes = await fetchCurrency(authToken)

  let transactionRes = null
  if (id) {
    transactionRes = await fetchTransaction(id, authToken)
    transactionRes = transactionRes?.data?.msg
  }
  return (
    <div className='flex flex-auto flex-col px-1'>
      <TransactionCreationComponent transactionData={transactionRes} currencyRes={currencyRes} />
    </div>
  )
}

export default page