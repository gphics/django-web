import { createContext } from "react";

export const ProfileContext = createContext();


export default function profileReducer(state, action) {
    switch (action.type) {
        case "TOGGLE_LOADING":
            return { ...state, isLoading: !state?.isLoading }
        default:
            return {...state}
    }
}