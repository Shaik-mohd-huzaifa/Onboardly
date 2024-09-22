import axios from "axios";

export const GetEmployees = async (orgId) => {
  try {
    const res = await axios.post("http://127.0.0.1:5000/getOrgsEmps", {
      org_id: orgId,
    });
    console.log(res.data);
    return res.data;
  } catch (error) {
    console.log(error);
  }
};
