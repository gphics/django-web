import ProfileUpdateComponent from "@/components/ProfileComponents/ProfileUpdateComponent"
import ProfileUpdateRenderer from "@/components/ProfileComponents/ProfileUpdateRenderer"
import UserUpdateComponent from "@/components/ProfileComponents/UserUpdateComponent"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"

export async function generateMetadata() {
  return { title: "Update Profile" }
}

async function fetchUserProfile(authToken) {
  const url = "account/profile"
  const res = await sendRequest(url, { providedAuthToken: authToken })

  return res
}

async function page() {

  const store = await cookies()
  const cookieMgt = CookieManager("server", store)
  const authToken = cookieMgt.getCookie()
  const res = await fetchUserProfile(authToken)
  const { user = null, ...profile } = res?.data?.msg || {}
  return (
    <div className='px-2 flex-auto flex flex-col'>
      {res?.err ? <h2 className="text-[1.5em] text-rose-500 poppins-bold text-center mt-10"> {res?.err?.[0]}   </h2> : <>
        <h2 className="text-center text-[1.3em] font-bold uppercase my-2">Profile Update</h2>
        <ProfileUpdateRenderer userData={user} profileData={profile} />
      </>}
    </div>
  )
}

export default page