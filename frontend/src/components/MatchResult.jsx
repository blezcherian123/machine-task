import "../css/MatchResult.css";

function MatchResult({ result }) {
  const isMatch = result.is_match;

  return (
    <div
      className={`match-result ${isMatch ? "is-match" : "not-match"}`}
      role="status"
    >
      <div className="result-heading">
        {isMatch ? "It's a Match!" : "Not a Match"}
      </div>
      <p className="result-message">{result.message}</p>
    </div>
  );
}

export default MatchResult;
