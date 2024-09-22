import { Link } from "react-router-dom";

export const SideBar = ({ option, header }) => {
  return (
    <div className="sidebar">
      <div className="header">
        <img src="/logo.jpg" alt="" />
        <h2>{header}</h2>
      </div>
      <ul>
        {option.map((opt, index) => (
          <li key={index}>
            <Link to={opt.path}>{opt.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};
