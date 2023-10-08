const salesDateInput = document.getElementById("sales_date");
const productSelect = document.getElementById("product-select");
const dateSelect = document.getElementById("sales_date");
const priceInput = document.getElementsByName("price")[0];
const discountInput = document.getElementsByName("discount")[0];
const commissionInput = document.getElementsByName("salesperson_commission")[0];

function getToday() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  let formattedDate = `${year}-${month}-${day}`;

  // get sales date
  if (document.getElementById("sales_date").value) {
    formattedDate = document.getElementById("sales_date").value;
  }

  return formattedDate;
}

async function getProductDetails(id) {
  try {
    const response = await fetch(`../api/product-details/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: id,
        sale_date: getToday(),
      }),
    });

    if (!response.ok) {
      throw new Error(`${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching product details:", error);
    return null;
  }
}

async function fetchPostRequest(url) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: id,
        sale_date: getToday(),
      }),
    });

    if (!response.ok) {
      throw new Error(`${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching product details:", error);
    return null;
  }
}

async function handleProductChange() {
  const selectedValue = productSelect.value;

  const data = await getProductDetails(selectedValue);
  if (data) {
    priceInput.value = data.sale_price;
    discountInput.value = -data.discount;
    commissionInput.value = data.commission;
  }
}

async function handleSaleDateChange() {
  console.log("date change")
  const salerdata = await fetchPostRequest("../api/product-details/");
  populateSalerByDate('salesperson', salerdata);

  const customerdata = await fetchPostRequest("../api/customer-details/");
  populateCustomerByDate('customer', customerdata);

  const selectedValue = productSelect.value;
  const pricedata = await getProductDetails(selectedValue);
  if (pricedata) {
    priceInput.value = pricedata.sale_price;
    discountInput.value = -pricedata.discount;
    commissionInput.value = pricedata.commission;
  }
}

function populateOptionByDate(select_id, data) {
  const salesperson_select = document.getElementById('customer')
  salesperson_select.innerHTML = ""
  for (let i = 0; i < data.length; i++) {
    const id = data[i][0]
    const last_name = data[i][2]
    const first_name = data[i][1]
    const phone = data[i][3]
    const option = document.createElement('option')
    option.setAttribute('value', id)
    option.innerHTML = `${last_name}, ${first_name} - ${phone}`
    salesperson_select.appendChild(option)
  }
}

productSelect.addEventListener("change", handleProductChange);
dateSelect.addEventListener("change", handleSaleDateChange);
document.addEventListener("DOMContentLoaded", async function () {
  salesDateInput.value = getToday();
  await handleProductChange();
});


