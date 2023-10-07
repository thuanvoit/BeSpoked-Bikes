const salesDateInput = document.getElementById("sales_date");
const productSelect = document.getElementById("product-select");
const priceInput = document.getElementsByName("price")[0];
const discountInput = document.getElementsByName("discount")[0];
const commissionInput = document.getElementsByName("salesperson_commission")[0];

function setToday() {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  const formattedDate = `${year}-${month}-${day}`;
  salesDateInput.value = formattedDate;
}

async function getProductDetails(id) {
  try {
    const response = await fetch(`../api/product-details/${id}`, {
      method: "GET",
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
    discountInput.value = data.discount;
    commissionInput.value = data.commission;
  }
}

productSelect.addEventListener("change", handleProductChange);
document.addEventListener("DOMContentLoaded", async function () {
  setToday();
  await handleProductChange();
});
