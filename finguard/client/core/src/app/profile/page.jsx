import MediaPresentationComponent from "@/components/Others/MediaPresentationComponent"
import PersonalInformationComponent from "@/components/ProfileComponents/PersonalInformationComponent"
import CookieManager from "@/utils/cookieManager"
import sendRequest from "@/utils/requestSender"
import { cookies } from "next/headers"
import Link from "next/link"
import { FaEdit } from "react-icons/fa"
import { FaCalendar } from "react-icons/fa6"
import { MdMail } from "react-icons/md"

export async function generateMetadata({ }) {
  return {
    title: "Profile"
  }
}

async function fetchProfile(authToken) {
  const url = "account/profile"
  const res = sendRequest(url, { providedAuthToken: authToken })
  return res
}

async function page() {

  const store = await cookies()
  const cookieMgt = CookieManager("server", store)
  const authToken = cookieMgt.getCookie()
  const profileRes = await fetchProfile(authToken)
  const data = profileRes?.data?.msg || null


  return (
    <div className='flex-auto flex flex-col px-2 items-center my-2'>
      {!data ? <h2 className="text-center text-[1.5em] text-rose-400 capitalize"> {profileRes?.err?.[0]}  </h2> : <>
        <header className="flex items-center justify-between my-2 w-full max-w-[650px]">

          <div>
            <h2 className="font-semibold">My Profile</h2>
            <p>Manage your personal information</p>
          </div>


          <Link className="text-white w-fit px-4 py-1 font-medium bg-primary-color rounded-sm" href={"/profile/edit"}> Edit Profile </Link>
        </header>

        <section className="self-center border rounded-md w-full max-w-[700px]">

          <div className="pl-10 bg-primary-color flex items-center text-white">
            <div className="flex flex-col items-center justify-around">
              <MediaPresentationComponent media={data?.media} name={data?.user?.username} />
              <Link className="text-[1.3em] mb-3 text-accent-color hover:text-white transition-all duration-300 hover:transform-[scale(1.2)]" href={"/media?type=user&id=" + data?.user?.id}> <FaEdit />  </Link>
            </div>

            <article className="ml-5 py-2">
              <h3 className="poppins-bold capitalize"> {data?.user?.username}  </h3>
              <h4 className="lowercase my-1"> {data?.user_type} </h4>
              <p className="flex items-center my-1">
                {!data?.user?.email ? "" : <>  <MdMail className="text-accent-color" size={28} /> <span className="ml-1 text-center"> {data?.user?.email}</span>  </>}

                <FaCalendar className="ml-2 text-accent-color" size={20} /> <span className=" ml-2 text-center">Joined {new Date(data?.created_at).toDateString()} </span>

              </p>
            </article>

          </div>

          {data && <PersonalInformationComponent data={data} />}
        </section>

      </>
      }
    </div>
  )
}

export default page