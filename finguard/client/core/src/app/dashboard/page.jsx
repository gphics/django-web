import TransactionRenderer from "@/components/DashboardComponent/TransactionRenderer"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"

async function getUserTransactions(providedAuthToken, page = 1, filters) {
  const url = "transaction/?page=" + page
  const res = await sendRequest(url, { providedAuthToken , filters})
  return res
}
 
async function getUserCurrency(providedAuthToken) {
  const url = "account/profile/currencies?user=yes"
  const res = await sendRequest(url, { providedAuthToken })
  return res
}

async function getUserFilteringLimit(providedAuthToken) {
  const url = "transaction/filtering-limit"
  const res = await sendRequest(url, { providedAuthToken })
  return res
}

export async function generateMetadata() {
  return { title: "Dashboard" }
}


async function page({ searchParams }) {

  const queryParams = await searchParams

  // getting the current page
  const currentPage = Number(queryParams?.page || 1)

  // getting filters if present
  const { page, ...rest } = queryParams
  const filters = rest || {}

  // getting server cookies
  const cookieStore = await cookies()

  // initiating cookie store
  const cookieMgt = CookieManager("server", cookieStore)

  // getting auth token
  const authToken = cookieMgt.getCookie()

  // fetching the transaction data
  const res = await getUserTransactions(authToken, currentPage, filters)

  const key = new URLSearchParams(queryParams).toString()
  console.log(key)
  // getting user currency code
  const userCurrencyRes = await getUserCurrency(authToken)

  // getting user filterig limit
  const filteringLimitRes = await getUserFilteringLimit(authToken)

  return (
    <div className='flex flex-auto px-2'>
      <TransactionRenderer key={key} result={res} filteringLimitRes={filteringLimitRes} currencyRes={userCurrencyRes} />
    </div>
  )
}


export default page