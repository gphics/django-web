import React from 'react'
import LoadingComponent from './LoadingComponent'

function FullPageLoadingComponent() {
  return (
      <div className='fixed flex justify-center items-center bg-overlay w-full h-screen top-[0] left-0 z-9999'>
          <LoadingComponent/>
    </div>
  )
}

export default FullPageLoadingComponent