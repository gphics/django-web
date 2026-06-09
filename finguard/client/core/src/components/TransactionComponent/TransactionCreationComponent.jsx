"use client"

import { useState } from "react"
import MonoCreationComponent from "./MonoCreationComponent"
import BulkCreationComponent from "./BulkCreationComponent"

function TransactionCreationComponent({ currencyRes, transactionData }) {

  const [creationType, setCreationType] = useState("mono")

  return (
    <div className="flex flex-col">

      {/* control */}
      <section className="py-2 flex justify-between w-[300px] self-center my-1 relative">
        <button className="bg-overlay w-17 py-1 cursor-pointer" type="button" onClick={()=>setCreationType("mono")}>Single</button>
        <button className="bg-overlay w-17 py-1 cursor-pointer" type="button" onClick={() => setCreationType("bulk")}>Bulk</button>

        {/* Bar .. */}
        <div className={"bg-accent-color w-17 absolute top-10 h-1 transition-all duration-200 " + (creationType === "mono" ? "left-0" : "left-[232px]")}></div>
      </section>

      {/* Forms */}
      {creationType === "mono" ? <MonoCreationComponent transactionData={transactionData} currency={currencyRes?.data?.msg?.currency || "$"} /> : <BulkCreationComponent/>}
    </div>
  )
}

export default TransactionCreationComponent