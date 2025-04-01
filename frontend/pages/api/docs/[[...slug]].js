// frontend/pages/api/docs/[[...slug]].js
import SwaggerUI from 'swagger-ui-react'
import 'swagger-ui-react/swagger-ui.css'

export default function Swagger({ spec }) {
  return <SwaggerUI spec={spec} />
}

export async function getServerSideProps(context) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/openapi.json`)
  const spec = await res.json()
  
  return {
    props: {
      spec
    }
  }
}