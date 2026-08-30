import "../css/CheckMatchLoading.css";

function CheckMatchLoading() {
  return (
    <div className="match-loading">
      <div className="heart-loader">
        <span>&#10084;</span>
        <span>&#10084;</span>
        <span>&#10084;</span>
      </div>
      <p className="loading-greeting">Finding your match...</p>
      <p className="loading-tips">All the best buddy!!</p>
    </div>
  );
}

export default CheckMatchLoading;
