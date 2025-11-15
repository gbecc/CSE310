using System;
using System.Collections.Generic;
using System.IO;

namespace InventoryApp
{
    class Program
    {
        static void Main()
        {
            // Load previously saved items from the file (stretch challenge)
            List<InventoryItem> products = LoadInventory();

            bool running = true;

            // Simple loop that allows a choice, and then utilizes the proper function
            while (running)
            {
                Console.WriteLine("==== Simple Inventory App ====");
                Console.WriteLine("1. Add product");
                Console.WriteLine("2. List products");
                Console.WriteLine("3. Quit");
                Console.Write("Choose an option (1-3): ");

                string? choice = Console.ReadLine();
                Console.WriteLine(); // blank line for spacing

                switch (choice)
                {
                    case "1":
                        AddProduct(products);
                        break;
                    case "2":
                        ListProducts(products);
                        break;
                    case "3":
                        // Save inventory on exit (stretch challenge)
                        SaveInventory(products);
                        running = false;
                        break;
                    default:
                        Console.WriteLine("Invalid option, please try again.\n");
                        break;
                }
            }

            Console.WriteLine("Goodbye!");
        }

        // This function asks the user for product info and adds it to the list
        static void AddProduct(List<InventoryItem> products)
        {
            Console.Write("Product name: ");
            string name = Console.ReadLine() ?? "";

            Console.Write("Quantity (whole number): ");
            int quantity = int.Parse(Console.ReadLine() ?? "0");

            Console.Write("Price per unit (for example 3.50): ");
            decimal price = decimal.Parse(Console.ReadLine() ?? "0");

            InventoryItem p = new Product(name, quantity, price);
            products.Add(p);

            Console.WriteLine("Product added!\n");
        }

        // This function prints all products and the total value
        static void ListProducts(List<InventoryItem> products)
        {
            if (products.Count == 0)
            {
                Console.WriteLine("No products in the inventory yet.\n");
                return;
            }

            Console.WriteLine("Current inventory:");
            decimal totalValue = 0;

            foreach (InventoryItem item in products)
            {
                Console.WriteLine(item);              // uses ToString from base
                totalValue += item.TotalValue;        // uses shared logic
            }

            Console.WriteLine($"Total inventory value: {totalValue:C}\n");
        }

        // STRETCH CHALLENGE -----------

        // Saves all products to inventory.txt
        static void SaveInventory(List<InventoryItem> products)
        {
            using (StreamWriter writer = new StreamWriter("inventory.txt"))
            {
                foreach (InventoryItem item in products)
                {
                    writer.WriteLine($"{item.Name}|{item.Quantity}|{item.PricePerUnit}");
                }
            }
        }

        // Loads products from inventory.txt (if it exists)
        static List<InventoryItem> LoadInventory()
        {
            List<InventoryItem> products = new List<InventoryItem>();

            if (!File.Exists("inventory.txt"))
                return products;

            foreach (string line in File.ReadAllLines("inventory.txt"))
            {
                string[] parts = line.Split('|');
                if (parts.Length != 3) continue;

                string name = parts[0];
                int quantity = int.Parse(parts[1]);
                decimal price = decimal.Parse(parts[2]);

                products.Add(new Product(name, quantity, price));
            }

            return products;
        }
    }

    abstract class InventoryItem
    {
        public string Name { get; }
        public int Quantity { get; }

        protected InventoryItem(string name, int quantity)
        {
            Name = name;
            Quantity = quantity;
        }

        // Derived classes MUST provide a price
        public abstract decimal PricePerUnit { get; }

        public decimal TotalValue => Quantity * PricePerUnit;

        public override string ToString()
        {
            return $"{Name} - Qty: {Quantity}, Price: {PricePerUnit:C}";
        }
    }

    class Product : InventoryItem
    {
        private decimal _pricePerUnit;

        public override decimal PricePerUnit => _pricePerUnit;

        public Product(string name, int quantity, decimal pricePerUnit)
            : base(name, quantity)
        {
            _pricePerUnit = pricePerUnit;
        }
    }
}
