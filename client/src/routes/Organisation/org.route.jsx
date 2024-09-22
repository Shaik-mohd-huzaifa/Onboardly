import { SideBar } from "../../components/sidebar/sidebar.component";
import sidebarData from "./../../../solid data/OrgSideBar.json";
import { Outlet } from "react-router";

export const OrganisationDashboard = () => {
  return (
    <div className="">
      <h2>Organisation Dashboard</h2>
      <SideBar header="Organisation Dashboard" option={sidebarData} />
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
};
