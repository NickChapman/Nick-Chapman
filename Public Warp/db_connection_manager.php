<?php
/**
 * Created by PhpStorm.
 * User: Blio
 * Date: 6/27/14
 * Time: 6:08 PM
 */

namespace warp_drive;

require 'user_settings.php';

/**
 * Class connection_manager
 * @package warp_drive
 */
class connection_manager {

    /**
     * Properties
     */
    private $host;
    private $username;
    private $password;
    private $database;
    private $connection;
    private $error_details;

    function __construct(){
        $this->host = DB_HOST;
        $this->username = DB_USERNAME;
        $this->password = DB_PASSWORD;
        $this->database = DATABASE;
    }

    function establish_database_connection(){
        switch(DATABASE_ENGINE){
            case "NoDB":
                $this->establish_nodb_connection();
                break;
            case "MySQLi":
                $this->establish_mysql_connection();
                break;
            default:
                throw new \Exception('Database engine set in `user_settings.php` is not currently supported. Check your spelling.');
        }
    }

    /**
     * Establishes a connection using the defined login credentials
     *
     * Returns false if credentials have not been set
     * Returns false and sets $error_details to the connection error number if the connection fails
     * Returns true and sets $connection to the db connection on success
     */
    function establish_mysql_connection(){
        $this->connection = new \mysqli($this->host, $this->username, $this->password, $this->password);
        if($this->connection->connect_errno){
            $this->error_details = $this->connection->connect_errno;
            unset($this->connection);
            throw new \Exception('MySQL connection failed. Database error number ' . $this->error_details . '. Check connection settings in `user_settings.php`');
        }
    }

    function establish_nodb_connection(){
        //TODO: Write something which will spin up a NoDB session
    }

} 