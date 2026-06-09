import { NextResponse } from "next/server";

export function proxy(request) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("token");
  const isPublicRoute = pathname === "/" || pathname.startsWith("/auth")

  // static path ...
  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.includes(".")
  ) {
    return NextResponse.next();
  }
  if ( isPublicRoute && token) {
    // special routes to ignore or checkout for
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // All other routes, the token is required
  if (!token && !isPublicRoute) {
  
    return NextResponse.redirect(new URL("/", request.url));
  }

  // if the token is present
  return NextResponse.next();
}

