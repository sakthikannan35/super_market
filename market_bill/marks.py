import pandas as dp
import smtplib
def stock(fd):
    print("Available Stocks Name :")
    for stocks in fd['stock name']:
        print(stocks)
def purchase_product(fd):
    cost = 0
    gst = 0.8
    billing_items = []
    while True:
        product_name = input("Enter the name of the product you want to buy (or 'exit' to exit): ")
        if product_name.lower() == 'exit':
            print("\nBill is Printing")
            break
        if product_name in fd['stock name'].values:
            product_details = fd[fd['stock name'] == product_name]
            while True:
                try:
                    how_many = int(input(f"How many {product_name} do you want to buy? "))
                    if how_many <= 0:
                        print("Please enter a valid quantity greater than zero.")
                    elif how_many > product_details['available quantity'].values[0]:
                        print(f"Sorry, we only have {product_details['available quantity'].values[0]} units available.")
                    else:
                        org_index = product_details.index[0]
                        fd.at[org_index, 'available quantity'] -= how_many
                        cost_per_unit = product_details['product price'].values[0]
                        total_product_cost = how_many * cost_per_unit
                        gst_amount = total_product_cost * gst
                        total_product_cost_with_gst = total_product_cost + gst_amount
                        cost += total_product_cost_with_gst
                        billing_items.append({"Product": product_name,
                                              "Quantity": how_many,
                                           "Price per unit": cost_per_unit,
                                           "GST Amount": gst_amount,
                                           "Total cost": total_product_cost_with_gst})
                        print(f"You can buy {how_many} {product_name} at ${cost_per_unit:.2f} each.")
                        print(f"Total cost for {how_many} {product_name} (incl. GST): ${total_product_cost_with_gst:.2f}")
                        break
                except ValueError:
                    print("Sorry,Invalid Input.Please Enter a Valid Number")
            else:
                print(f"Product '{product_name}' not found. Please enter a valid product name.")
        if billing_items:
            print("\nBill")
        for item in billing_items:
            print(f"{item['Quantity']} {item['Product']} at ${item['Price per unit']:.2f} each. Total (incl. GST): ${item['Total cost']:.2f}")
            print(f"  GST Amount: ${item['GST Amount']:.2f}")
        print(f"\nTotal Bill Amount (incl. GST): ${cost:.2f}")
        fd.to_csv('stocks.csv', index=False)
        print("Stock file updated.")
        enter_mail = input("Enter email id to get bill (or 'exit' to exit): ")
        if enter_mail.lower() == 'exit':
            return  
        mails(enter_mail, billing_items, cost)
    else:
        print("No items purchased. Exiting...")
        print("Thank you for shopping with us!")
def mails(enter_mail, bill_items, cost):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('sakthikannan305@gmail.com', 'tucg qwgw oxeg tldc')
        subject = 'Your Purchase Bill'
        head = "\nBill Summary\n"
        for item in bill_items:
            head += f"{item['Quantity']} {item['Product']} at ${item['Price per unit']:.2f} each. Total: ${item['Total cost']:.2f}\n"
            head += f"  GST Amount: ${item['GST Amount']:.2f}\n"
        head += f"\nTotal Bill Amount (incl. GST): ${cost:.2f}"
        message = f"Subject: {subject}\n\n{head}"
        smtp_server.sendmail('sakthikannan305@gmail.com', enter_mail, message)
        smtp_server.quit()
        print(f"Bill sent successfully to {enter_mail}")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
def main():
    fd = dp.read_csv('stocks.csv')
    stock(fd)
    while True:
        purchase_product(fd)
        next_customer = input("Do you want to continue with another customer? (yes/no): ")
        if next_customer.lower() != 'yes':
            break
    print("Thank you for using our shopping system!")
if __name__ == "__main__":
    main()                   