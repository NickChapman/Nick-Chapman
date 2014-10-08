<?php
/**
 * Created by PhpStorm.
 * User: Blio
 * Date: 6/27/14
 * Time: 6:46 PM
 */

/**
 * This file contains all of the user settings.
 *
 * Some settings are preceded by a list of appropriate values if its a tricky setting.
 *      Feel free to mess around with the settings to your heart's content but know that some settings are really easy to get wrong
 *      If you mess up the settings don't forget that you can always download the user_settings.php file from WarpCode.org
 * Settings with improper values will make it impossible for the warp drive to start.
 *
 * In the future there will be a settings authenticator but for now it is on you to choose the appropriate settings
 */

/**
 * STORAGE SETTINGS
 * Currently supported databases are:
 *  NoDB - Warp's storage engine, runs off local files.
 * Coming soon:
 *  MySQLi (note the i)
 */
const DATABASE_ENGINE = 'NoDB';

//NoDB Options
const STORAGE_LOCATION = 'Warp/post_storage/';

//Remote Database Options
const DB_USERNAME = "user";
const DB_PASSWORD = "pass";
const DB_HOST = "localhost";
const DATABASE = "test";

/**
 * POST CREATOR DEFAULTS
 */

// LANGUAGE does nothing at present. It is simply data being collected for potential use in the post_creator class
const LANGUAGE = "en";
// !!!! CHANGE !!!! Should be your name or the site owners name
const CREATOR = "Warp";