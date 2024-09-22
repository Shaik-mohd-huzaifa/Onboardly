import { createBrowserRouter } from "react-router-dom";
import { EmployeeDashboard } from "./Employee/employee.route";
import { OrganisationDashboard } from "./Organisation/org.route";
import { SignUp } from "../components/SignUp/SignUp.component";
import { Profile } from "../components/Profile/Profile.component";
import a from "../../solid data/a.json";
import { EmployeePage } from "../components/Employee Page/EmployeePath.component";
import { DocumentUploads } from "../components/Documents/documents.component";
import AddNotes from "../components/AddNotes/AddNotes.component";

export const Router = createBrowserRouter([
  {
    path: "/",
    element: "Hello World",
    errorElement: "404",
  },
  {
    path: "/employeeDashboard",
    element: <EmployeeDashboard />,
  },
  {
    path: "/orgDashboard",
    element: <OrganisationDashboard />,
    children: [
      {
        index: true,
        element: <Profile info={a} />,
      },
      {
        path: "employees",
        element: <EmployeePage />,
      },
      {
        path: "documents",
        element: <DocumentUploads />,
      },
      {
        path: "rules",
        element: <AddNotes />,
      },
    ],
  },
  {
    path: "/signup",
    element: <SignUp />,
  },
]);
