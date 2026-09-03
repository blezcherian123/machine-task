import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import CheckMatchLoading from "./CheckMatchLoading";
import MatchResult from "./MatchResult";
import "../css/Dashboard.css";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function onlyLetters(value) {
  return value.replace(/[^A-Za-z ]/g, "").replace(/ {2,}/g, " ");
}

function getFirstName(user) {
  if (!user) return "";
  const fullName = user.full_name?.trim();
  if (fullName) return fullName.split(" ")[0];
  const email = user.email?.trim();
  if (email) return email.split("@")[0];
  return "";
}

function Dashboard() {
  const navigate = useNavigate();
  const storedUser = localStorage.getItem("user");
  let user = null;
  if (storedUser) {
    try {
      user = JSON.parse(storedUser);
    } catch {
      user = null;
    }
  }

  const [boyName, setBoyName] = useState("");
  const [girlName, setGirlName] = useState("");
  const [error, setError] = useState("");
  const [checking, setChecking] = useState(false);
  const [result, setResult] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }
  }, [token, navigate]);

  const namesPresent = () => boyName.trim() && girlName.trim();

  const handleCheckMatch = async () => {
    setError("");
    setResult(null);
    if (!namesPresent()) {
      setError("Please enter both a boy name and a girl name.");
      return;
    }
    setChecking(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/auth/check-match`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          boy_name: boyName.trim(),
          girl_name: girlName.trim(),
        }),
      });
      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(errData?.detail || "Could not check the match.");
      }
      const data = await response.json();
      await new Promise((resolve) => setTimeout(resolve, 3000));
      setResult(data);
    } catch (err) {
      setError(err.message || "Could not check the match.");
    } finally {
      setChecking(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const handleDeleteAccount = async () => {
    const confirmed = window.confirm(
      "Are you sure you want to permanently delete your account? This action cannot be undone."
    );
    if (!confirmed) return;
    setError("");
    setChecking(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/auth/me`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error("Could not delete the account. Please try again.");
      }
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      navigate("/login");
    } catch (err) {
      setError(err.message || "Could not delete the account.");
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="dashboard-logo">
          match<span>.com</span>
        </div>
        <div className="dashboard-actions">
          <button
            className="dashboard-delete"
            onClick={handleDeleteAccount}
            disabled={checking}
          >
            Delete Account
          </button>
          <button className="dashboard-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <h1>Welcome{getFirstName(user) ? `, ${getFirstName(user)}` : ""}!</h1>
        <p className="dashboard-subtitle">Your surprise match awaits</p>

        <div className="match-card">
          <h2>Welcome to Match.com surprise app</h2>
          <p className="match-card-subtitle">
            Enter the two names, then check if it&apos;s a match. Only letters are
            allowed.
          </p>

          <div className="match-form">
            <div className="form-group">
              <label htmlFor="boyName">Boy Name</label>
              <input
                id="boyName"
                type="text"
                value={boyName}
                onChange={(e) => setBoyName(onlyLetters(e.target.value))}
                placeholder="Enter boy's name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="girlName">Girl Name</label>
              <input
                id="girlName"
                type="text"
                value={girlName}
                onChange={(e) => setGirlName(onlyLetters(e.target.value))}
                placeholder="Enter girl's name"
              />
            </div>

            {error && <div className="match-error">{error}</div>}

            <button
              type="button"
              className="match-button"
              onClick={handleCheckMatch}
              disabled={checking}
            >
              {checking ? "Checking..." : "Check Match"}
            </button>
          </div>

          {checking && <CheckMatchLoading />}

          {result && !checking && <MatchResult result={result} />}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
