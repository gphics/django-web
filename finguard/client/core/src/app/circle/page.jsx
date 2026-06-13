import CircleRendererComponent from "@/components/CircleComponents/CircleRendererComponent"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"


export async function generateMetadata() {
  return {
    title: "User | Circle "
  }
}

async function fetchCircle(authToken) {
  const res = await sendRequest("transaction/circle", { providedAuthToken: authToken })
  return res
}
async function fetchPendingInvitation(authToken) {
  const res = await sendRequest("transaction/circle-invite", { providedAuthToken: authToken })
  return res
}

async function page() {

  const store = await cookies()

  const cookieMgt = CookieManager("server", store)

  const authToken = cookieMgt.getCookie()

  const invitationRes = await fetchPendingInvitation(authToken)
  const circleRes = await fetchCircle(authToken)


  return (
    <div className="px-1 flex flex-col flex-auto">
      <CircleRendererComponent circleRes={circleRes} pendingRes={invitationRes}  />
    </div>
  )
}

export default page