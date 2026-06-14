"use client"
import sendRequest from "@/utils/requestSender"
import { useContext, useState } from "react"
import { toast } from "react-toastify"
import { ProfileContext } from "./profileReducer"
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent"
function ProfileUpdateComponent() {

  const { state, dispatch } = useContext(ProfileContext)
  const [data, setData] = useState({
    user: {
      first_name: state.user?.first_name || "",
      last_name: state.user?.last_name || "",
    },
    profile: {
      country: state.profile?.country || "",
      state: state.profile?.state || "",
      city: state.profile?.city || "",
    },
    currency:""
  })

  
  const userItemArr = Object.entries(data?.user)
  const profileItemArr = Object.entries(data?.profile)

  async function updateInfo(e) {
    e.preventDefault()
    
    // updating isLoading
    dispatch({ type: "TOGGLE_LOADING" })

    const url = "account/profile"
    const { user, profile } = data
    const body = {user, profile:{...profile, currency:data?.currency}}
    const method = "PUT"
    const res = await sendRequest(url, { method, body })

    // updating isLoading
    dispatch({ type: "TOGGLE_LOADING" })


    if (res?.err || !res.success) {
      toast.error(res?.err?.[0])
      return
    }

    toast.success(res?.data?.msg)
    state?.refresh()
  }


  return (
    <form onSubmit={updateInfo} className="my-2 w-full max-w-[400px] mx-auto">
{/* <FullPageLoadingComponent/> */}
      <fieldset className="border-2 flex flex-col rounded-md">
        <legend className="text-center font-medium px-3">Profile Update Form</legend>

        {/* User Updates ... */}
        {userItemArr.map((elem, i) => {
          return <div className="flex flex-col" key={i}>

            <label className="w-[95%] font-medium my-1 capitalize mx-auto" htmlFor={elem[0]}> {elem[0].replace("_", " ")} </label>

            <input onChange={(e) => {
              const { name, value } = e.target
              const user = { ...data?.user, [name]: value }
              setData(prev => ({ ...prev, user }))
            }}
              type="text" name={elem[0]} value={data?.user?.[elem[0]]} className="bg-primary-color w-[95%] mx-auto h-[45px] outline-none font-medium border-none text-white rounded-sm my-1 px-2 focus:bg-accent-color focus:text-primary-color transition-all duration-200" placeholder={elem[0].replace("_", " ") + " ..."} />
          </div>
        })}

        {/* Profile Updates ... */}
        {profileItemArr.map((elem, i) => {
          return <div className="flex flex-col" key={i}>

            <label className="w-[95%] font-medium my-1 capitalize mx-auto" htmlFor={elem[0]}> {elem[0].replace("_", " ")} </label>

            <input onChange={(e) => {
              const {name, value} = e.target
              const profile = { ...data?.profile, [name]: value }
              setData(prev =>({...prev, profile}))
            }}
              type="text" name={elem[0]} value={data?.profile?.[elem[0]]} className="bg-primary-color w-[95%] mx-auto h-[45px] outline-none font-medium border-none text-white rounded-sm my-1 px-2 focus:bg-accent-color focus:text-primary-color transition-all duration-200" placeholder={elem[0].replace("_", " ") + " ..."} />
          </div>
        })}

        {/* Currency Update */}
        <div className="flex flex-col">

          <label className="w-[95%] font-medium my-1 capitalize mx-auto" htmlFor="currency_code"> Currency Code  </label>

          <input onChange={(e) => {
            const {  value } = e.target
            
            setData(prev => ({ ...prev, currency:value }))
          }}
            type="text" name="currency_code" value={data?.currency} className="bg-primary-color w-[95%] mx-auto h-[45px] outline-none font-medium border-none text-white rounded-sm my-1 px-2 focus:bg-accent-color focus:text-primary-color transition-all duration-200" placeholder="Currency code ..." />
        </div>

        {/* Submit btn */}
        <button type="submit" className="my-2 mx-auto font-medium bg-accent-color w-fit px-5 py-2 cursor-pointer text-white  rounded-md hover:bg-primary-color transition-all duration-200">Submit</button>
      </fieldset>

    </form>
  )
}

export default ProfileUpdateComponent





