"use client"
import { ToastContainer } from "react-toastify"
import { useRouter } from "next/navigation"
import { useReducer} from "react"

import FullPageLoadingComponent from "../Others/FullPageLoadingComponent"
import UserUpdateComponent from "./UserUpdateComponent"
import profileReducer, { ProfileContext } from "./profileReducer"
import ProfileUpdateComponent from "./ProfileUpdateComponent"

function ProfileUpdateRenderer({ profileData, userData }) {
    const router = useRouter()

    function triggerPageRefresh() {
        router.refresh()
    }
    const initialState = {
        isLoading: false,
        refresh: triggerPageRefresh,
        user: userData,
        profile:profileData
    }
    const [state, dispatch] = useReducer(profileReducer, initialState)
    return (
        <ProfileContext.Provider value={{state, dispatch}}>

            {!!state?.isLoading && <FullPageLoadingComponent />}
            <ToastContainer position="top-center" theme="dark" />
            <UserUpdateComponent />
            <ProfileUpdateComponent/>

        </ProfileContext.Provider>

    )
}



export default ProfileUpdateRenderer