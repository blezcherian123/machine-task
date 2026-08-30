import { Outlet, useLocation } from "react-router-dom";
import "../css/LoginPage.css";

function AuthLayout() {
  const { pathname } = useLocation();
  const mode = pathname.includes("/signup") ? "signup-mode" : "login-mode";

  return (
    <div className={`auth-container ${mode}`}>
      <div className="auth-branding">
        <h2>MEET YOUR MATCH</h2>
        <div className="logo">match<span className="logo-surprise">.com</span></div>
        <p>Join millions and find your perfect surprise — the spark you never knew you were looking for</p>
      </div>

      <div className="auth-form-container">
        <div className="auth-card">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default AuthLayout;
