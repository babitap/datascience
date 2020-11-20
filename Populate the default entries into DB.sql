use app_dev_db; 

---------------------------------------------------------------------------------------------------
-- add to subscription 
---------------------------------------------------------------------------------------------------
delete from app_dev_db.dbo.Accounts_subscription; 
INSERT INTO app_dev_db.dbo.Accounts_subscription("name", "description", "expire_date", "is_active") 
VALUES ( 'Administrator', 'Administrator', '2050-12-31', 1);
INSERT INTO app_dev_db.dbo.Accounts_subscription("name", "description", "expire_date", "is_active") 
VALUES ( 'TCS', 'TCS - St Anne & St James', '2020-12-31', 1);
select * from app_dev_db.dbo.Accounts_subscription;



