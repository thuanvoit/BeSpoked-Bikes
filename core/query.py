query_all_sales = """
                SELECT 	p.name as product_name, 
                        sp.first_name as sp_first_name, 
                        sp.last_name as sp_last_name, 
                        sp.phone as sp_phone, 
                        c.first_name as c_first_name, 
                        c.last_name as c_last_name, 
                        c.phone as c_phone,
                        s.sales_date, 
                        s.price, 
                        s.salesperson_commission 
                FROM core_sale as s
                LEFT JOIN core_product as p
                ON s.product_id = p.id
                LEFT join core_salesperson as sp
                on s.salesperson_id = sp.id
                LEFT join core_customer as c
                on s.customer_id = c.id;
            """
            
query_sale_by_date_range = """
                SELECT 	p.name as product_name, 
                        sp.first_name as sp_first_name, 
                        sp.last_name as sp_last_name, 
                        sp.phone as sp_phone, 
                        c.first_name as c_first_name, 
                        c.last_name as c_last_name, 
                        c.phone as c_phone,
                        s.sales_date, 
                        s.price, 
                        s.salesperson_commission 
                FROM core_sale as s
                LEFT JOIN core_product as p
                ON s.product_id = p.id
                LEFT join core_salesperson as sp
                on s.salesperson_id = sp.id
                LEFT join core_customer as c
                on s.customer_id = c.id
                where %s <= s.sales_date 
                and s.sales_date <= %s;
            """

query_saler_by_sale_date = """
                select sp.id, sp.first_name, sp.last_name, sp.phone
                from core_salesperson as sp
                where sp.start_date <= %s
                AND (sp.termination_date IS NULL 
                    OR %s <= sp.termination_date);
                        """

query_customer_by_sale_date = """
                select c.id, c.first_name, c.last_name, c.phone, c.start_date
                from core_customer as c
                where c.start_date <= %s;
                        """

query_sale_report_quarterly = """
            SELECT sp.id AS salesperson_id, sp.first_name, sp.last_name, 
                sp.phone as phone, ROUND(SUM(s.price)) AS revenue, 
                ROUND(SUM(s.salesperson_commission), 2) AS commission, 
                COUNT(s.product_id) AS total_product, s.sales_date, 
                (EXTRACT(QUARTER FROM s.sales_date)) as quarter,
                (EXTRACT(YEAR FROM s.sales_date)) as year
                            
            FROM core_salesperson AS sp 
            LEFT JOIN core_sale AS s ON s.salesperson_id = sp.id
                        
            WHERE (EXTRACT(YEAR FROM s.sales_date) = %s) AND (EXTRACT(QUARTER FROM s.sales_date) = %s)
            GROUP BY sp.id, sp.first_name, sp.last_name, sp.phone, s.sales_date;

        """