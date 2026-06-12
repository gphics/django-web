import MemberInvitationComponent from "@/components/CircleComponents/SingleCircle/MemberInvitationComponent"
import SingleCircleHomeComponent from "@/components/CircleComponents/SingleCircle/SingleCircleHomeComponent"
import SingleCircleInfoComponent from "@/components/CircleComponents/SingleCircle/SingleCircleInfoComponent"
import SingleCircleRenderer from "@/components/CircleComponents/SingleCircle/SingleCircleRenderer"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"


export async function generateMetadata({ params }) {
  const { id } = await params
  return {
    title: "Circle | " + id
  }
}

async function fetchMemberRole(circleId, authToken) {
  const url = "transaction/circle-member-role?circle=" + circleId
  const res = await sendRequest(url, { providedAuthToken: authToken })
  return res
}

async function page({ params, searchParams }) {
  const { id } = await params
  // Home, Info, Invitation
  const currentView = (await searchParams)?.view || "Home"

  // cookie ....
  const store = await cookies()
  const cookieMgt = CookieManager("server", store)
  const authToken = cookieMgt.getCookie()

  const memberRoleRes = await fetchMemberRole(id, authToken)
  const memberRole = memberRoleRes?.data?.msg || null

  const adminArr = ["ADMIN", "OWNER"]
  const isAdmin = adminArr.includes(memberRole)
  
  return (
    <div className='flex-auto flex flex-col px-1'>
      {!memberRoleRes?.success || memberRoleRes?.err ? <h2 className="self-center mx-auto text-[1.3me] text-rose-500 poppins-bold"> memberRoleRes?.err[0] </h2> : <> 
        
        {/* Navigation */}
      <SingleCircleRenderer isAdmin={isAdmin} circleId={id} currentView={currentView} />

      {/* Rendering view conditionally */}
      {currentView === "Home" && <SingleCircleHomeComponent authToken={authToken} circleId={id} />}
        {currentView === "Info" && <SingleCircleInfoComponent authToken={authToken} circleId={id} />}
        
        {/* Visible to only the admin */}
      {isAdmin && currentView === "Invitation" && <MemberInvitationComponent authToken={authToken} circleId={id} />}

      </>}
    </div>
  )
}

export default page