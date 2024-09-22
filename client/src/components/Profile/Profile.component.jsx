import { useSelector } from "react-redux";
import { organisationSelector } from "../../store/Organisation/organisation.selector";
import { useState } from "react";

export const Profile = () => {
  const data = useSelector(organisationSelector);
  const [org, setOrg] = useState(data);

  const formatTitle = (key) => {
    return key
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  return (
    <div className="">
      {Object.entries(org).map(([key, value]) => (
        <div className="" key={key}>
          <p className="title">{formatTitle(key)}</p>
          <p className="value">{value}</p>
        </div>
      ))}
    </div>
  );
};
