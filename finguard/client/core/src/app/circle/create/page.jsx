import CircleCreationComponent from "@/components/CircleComponents/CircleCreationComponent"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"


export async function generateMetadata({ searchParams }) {

    const { id } = await searchParams
    return {
        title: id ? ("Update Circle |" + id) : "Create Circle"
    }
}

async function fetchCircle(circleId, authToken) {
    const url = "transaction/circle?id=" + circleId
    const res = await sendRequest(url, { providedAuthToken: authToken })
    return res
}
async function page({ searchParams }) {
    const { id } = await searchParams

    const store = await cookies()
    const cookieMgt = CookieManager("server", store)
    const authToken = cookieMgt.getCookie()

    const circleRes = await fetchCircle(id, authToken)
    const circleData = circleRes?.data?.msg || null
  
    return (
        <div className="flex-auto flex flex-col px-1">
            <CircleCreationComponent circleData={circleData}   />
        </div>
    )
}

export default page