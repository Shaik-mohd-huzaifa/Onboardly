import axios from "axios";

export const get_Documents = async (org_id) => {
  try {
    const res = await axios.post("http://127.0.0.1:5000/getDocs", {
      org_id: org_id,
    });
    return res.data;
  } catch (error) {
    console.log(error);
  }
};
