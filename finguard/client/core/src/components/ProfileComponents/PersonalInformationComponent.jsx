"use client"
export default function PersonalInformationComponent({ data }) {
    const userData = {
        username: data?.user?.username,
        email: data?.user?.email,
        first_name: data?.user?.first_name,
        last_name: data?.user?.last_name,
    }

    const profileData = {
        city: data?.city,
        country: data?.country,
        state: data?.state,
        contact: data?.contact,
      
    }

    const summaryStatData = {
        "mean": data?.summary_statistics["mean"],
        "min": data?.summary_statistics["min"],
        "max": data?.summary_statistics["max"],
        "std": data?.summary_statistics["std"],
        "25%": data?.summary_statistics["25%"],
        "50%": data?.summary_statistics["50%"],
        "75%": data?.summary_statistics["75%"],
        financial_activity: data?.financial_activity,
        number_of_transactions: data?.number_of_transactions,


    }
    const userCurrency = data?.currency
    const userDataArr = Object.entries(userData)
    const profileDataArr = Object.entries(profileData)
    const summaryStatDataArr = Object.entries(summaryStatData)
    return (
        <div className="flex flex-col justify-center items-center mb-2" >

            {/* User data */}
            <h3 className="my-1 poppins-bold uppercase">User </h3>
            <section className="flex flex-wrap justify-center items-center">
                {userDataArr.map((elem, i) => {
                    const key = elem[0]
                    const value = elem[1] || ""
                    return <article key={i} className="flex m-2 flex-col my-1  \ p-2">
                        <label htmlFor={key} className="capitalize my-1"> {key} </label>
                        <input placeholder={key + "..."} name={key} disabled={true} value={value} className="border rounded-md h-10 px-2 min-w-[300px] w-full" />
                    </article>
                })}
            </section>

            {/* Profile data */}
            <h3 className="my-1 poppins-bold uppercase">Profile </h3>
            <section className="flex flex-wrap justify-center items-center">
                {profileDataArr.map((elem, i) => {
                    const key = elem[0]
                    const value = elem[1] || ""
                    return <article key={i} className="flex m-2 flex-col my-1  \ p-2">
                        <label htmlFor={key} className="capitalize my-1"> {key} </label>
                        <input placeholder={key + "..."} name={key} disabled={true} value={value} className="border rounded-md h-10 px-2 min-w-[300px] w-full" />
                    </article>
                })}
            </section>

            {/* Summary transaction data */}
            <h3 className="my-1 poppins-bold uppercase">Summary Statistics </h3>
            <section className="flex flex-wrap justify-center items-center">
                {summaryStatDataArr.map((elem, i) => {
                    const key = elem[0]
                    const value = elem[1] || ""
                    return <article key={i} className="flex m-2 flex-col my-1  \ p-2">
                        <label htmlFor={key} className="capitalize my-1"> {key} </label>
                        <input placeholder={key + "..."} name={key} disabled={true} value={userCurrency + value} className="border rounded-md h-10 px-2 min-w-[300px] w-full" />
                    </article>
                })}
            </section>
        </div>
    )
}
