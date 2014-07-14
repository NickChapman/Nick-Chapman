<?php
/**
 * Created by PhpStorm.
 * User: Nick
 * Date: 7/5/14
 * Time: 6:10 PM
 */

namespace warp_drive;

require "user_settings.php";

class nodb {
    //TODO: Create a nodb first time setup page
    //TODO: Make something which lets you move something out of the post history and into some kind of holding stack.

    /**
     * METHODS
     */

    /**
     * Creates the files necessary for nodb to function and checks that both are writable
     *
     * @throws \Exception
     */
    static function first_time_setup(){
        //Make sure that first time setup has not been run before
        if(file_exists(STORAGE_LOCATION."nodb.hist") || file_exists(STORAGE_LOCATION."post_id.json")){
            throw new \Exception('First time setup has already been performed.');
        }
        $post_id = json_encode(["post_id" => 1]);
        $post_history = serialize(
            array(array("title" => "Example", "author" => "John Warp"))
        );
        if(!is_dir(STORAGE_LOCATION)){
            mkdir(STORAGE_LOCATION);
        }
        file_put_contents(STORAGE_LOCATION."post_id.json", $post_id);
        file_put_contents(STORAGE_LOCATION."nodb.hist", $post_history);
        file_put_contents(STORAGE_LOCATION."nodb.hist", '');
    }

    /**
     * Throws an exception if first time setup has not been performed or needed files are missing
     *
     * @throws \Exception
     */
    static function check_setup_status(){
        if(!file_exists(STORAGE_LOCATION."nodb.hist") || !file_exists(STORAGE_LOCATION."post_id.json")){
            throw new \Exception('First time setup needs to be performed or files are missing. For setup open nodb_setup.php or run nodb::first_time_setup');
        }
    }

    /**
     * This function will set the post_id.json file so that it points past the end of the post history and to an available post#
     *
     */
    static function verify_post_id_pointer(){
        nodb::check_setup_status();
        $post_history = unserialize(file_get_contents(STORAGE_LOCATION."post.hist"));
        $post_id = json_decode(file_get_contents(STORAGE_LOCATION."post_id.json"))["post_id"];
        $last_key = key(end($post_history));
        while(!($last_key < $post_id) || file_exists(STORAGE_LOCATION.strval($post_id).".json")){
            $post_id += 1;
        }
        file_put_contents(STORAGE_LOCATION."post_id.json", json_encode(array("post_id" => $post_id)));
    }

    /**
     * Checks to make sure that each post in the specified STORAGE_LOCATION is included in the post history.
     * If $print_list is true then a list of the unlogged posts is printed. Otherwise only an error is thrown.
     *
     * @throws \Exception
     */
    static function verify_stored_posts_against_history($print_list = false){
        nodb::check_setup_status();
        $posts = glob(STORAGE_LOCATION."[0-9]*.json");
        $post_history = unserialize(file_get_contents(STORAGE_LOCATION."nodb.hist"));
        $unlogged_posts = false;
        //Check that all stored posts are in the history
        foreach($posts as $post){
            $temp = explode('.', $post)[0];
            $temp = end(explode('/', $temp));
            if(!isset($post_history[$temp])){
                $unlogged_posts = true;
                if($print_list){
                    echo "$post is not in the post history\n";
                }
            }
        }
        if($unlogged_posts){
            throw new \Exception("Unlogged posts were detected in the post storage location");
        }
    }

    /**
     * Deletes every post file which is not included in the post history
     * !!!WARNING!!! This is a drastic action.
     * Please use nodb::verify_stored_posts_against_history(true) to inspect unlogged posts to make sure that you don't need them any more
     */
    static function clean_storage_location_of_old_posts(){
        nodb::check_setup_status();
        $posts = glob(STORAGE_LOCATION."[0-9]*.json");
        $post_history = unserialize(file_get_contents(STORAGE_LOCATION."nodb.hist"));
        //Check that all stored posts are in the history
        foreach($posts as $post){
            $temp = explode('.', $post)[0];
            $temp = end(explode('/', $temp));
            if(!isset($post_history[$temp])){
                unlink($post);
            }
        }
        echo STORAGE_LOCATION." Has been cleaned of unlogged posts";
    }

    /**
     * Saves a post data array to a json file with the name POST#.json
     * WARNING - Fails on overwrite. To overwrite a file use the update_post_data function
     * @param $post_data_array
     * @throws \Exception
     */
    function save_post($post_data_array){
        $this->check_setup_status();
        //Get the post id number to be used from post_id.json. This is broken apart to try and help you understand what happens here
        $post_id = strval(
            json_decode(
                file_get_contents(STORAGE_LOCATION."post_id.json")
            )[post_id]
        );
        //Check that the file we are going to write to doesn't exist yet
        if(file_exists(STORAGE_LOCATION.$post_id.".json")){
            throw new \Exception('The post id set in `post_id.json` has already been used. Run nodb::verify_post_id_pointer or to update posts use update_post_data');
        }
        //Encode the data to be saved
        $json_data = json_encode($post_data_array);
        //Save the data to $storage_location.$post_id.".json"
        file_put_contents(STORAGE_LOCATION.$post_id.".json", $json_data);
        //Add the current post_id to the post history list
        $this->add_post_to_history($post_data_array);
        echo "Post saved as $post_id.json";
        //Increment the post id counter
        $post_id += 1;
        $post_id_json = json_encode(array("post_id" => $post_id));
        file_put_contents(STORAGE_LOCATION."post_id.json", $post_id_json);
    }

    /**
     * Loads a preexisting post, saves it, and then ERASES the old file from disk if $erase = true
     *
     * @param      $post_file_path
     * @param bool $erase
     * @throws \Exception
     */
    function save_preexisting_post($post_file_path, $erase = false){
        if(!file_exists($post_file_path)){
            throw new \Exception("The post you are trying to save could not be found. Check your file path");
        }
        if(pathinfo($post_file_path)["extension"] != "json"){
            throw new \Exception("The post you are trying to save is not in the correct format");
        }
        $post_data_array = json_decode(file_get_contents($post_file_path));
        //Check that what we just loaded isn't empty
        if(trim($post_data_array) == ""){
            throw new \Exception("The post specified is empty");
        }
        $this->save_post($post_data_array);
        if($erase){
            unlink($post_file_path);
        }
    }

    /**
     * Loads and returns a post data array based on the id# provided
     *
     * @param $post_id - The id# of the post you want to load
     * @throws \Exception - No specific types, just make sure you catch them
     * @return Array - An array of the post data
     */
    function load_post_data_array($post_id){
        $this->check_setup_status();
        $post_id = strval($post_id);
        //Make sure the file even exists
        if(!file_exists(STORAGE_LOCATION.$post_id.".json")){
            throw new \Exception("Post requested does not exist");
        }
        //Load the json out of POST#.json
        $post_data_json = file_get_contents(STORAGE_LOCATION.$post_id.".json");
        //Check that what we just loaded isn't empty
        if(trim($post_data_json) == ""){
            throw new \Exception("The post specified is empty");
        }
        return json_decode($post_data_json);
    }

    /**
     * Updates a post entry using a new post_data_array and the post_id.
     * Cannot create a new post. Can only update them. Use save_post to create new posts.
     *
     * @param $post_data_array
     * @param $post_id
     * @throws \Exception
     */
    function update_post_data($post_data_array, $post_id){
        $this->check_setup_status();
        $post_id_string = strval($post_id);
        //If the post exists, overwrite its old data
        if(file_exists(STORAGE_LOCATION.$post_id_string.".json")){
            file_put_contents(STORAGE_LOCATION.$post_id_string.".json", serialize($post_data_array));
        }
        else{
            throw new \Exception('The post you are attempting to update does not appear to exist. Use nodb::save_post for saving new posts');
        }
        //Edit the post history so that the author and title are correct
        $post_history = unserialize(
            file_get_contents(STORAGE_LOCATION."nodb.hist")
        );
        $post_history[$post_id]["author"] = $post_data_array["author"];
        $post_history[$post_id]["title"] = $post_data_array["title"];
        //Write the new post history to disk
        file_put_contents(STORAGE_LOCATION."nodb.hist", serialize($post_history));
    }

    /**
     * @param $post_id
     * @throws \Exception
     */
    function delete_post($post_id){
        $post_id_string = strval($post_id);
        //Check that the file we want to delete exists
        if(!is_file(STORAGE_LOCATION.$post_id_string.".json")){
            throw new \Exception('The post you are trying to delete does not exist or could not be found');
        }
        else{
            unlink(STORAGE_LOCATION.$post_id_string.".json");
            $this->delete_post_from_history($post_id);
        }
    }

    /**
     * @param $post_data_array
     */
    function add_post_to_history($post_data_array){
        $this->check_setup_status();
        //Gets the post history
        $post_history = unserialize(file_get_contents(STORAGE_LOCATION."nodb.hist"));
        //Gets the post_id
        $post_id = json_decode(file_get_contents(STORAGE_LOCATION."post_id.json"), true)["post_id"];
        $title = $post_data_array["title"];
        $author = $post_data_array["author"];
        $post_history_entry = array("title" => $title, "author" => $author);
        $post_history[$post_id] = $post_history_entry;
        file_put_contents(STORAGE_LOCATION."nodb.hist", serialize($post_history));
    }

    /**
     * @param $post_id
     * @throws \Exception
     */
    function delete_post_from_history($post_id){
        $this->check_setup_status();
        //Get the post history
        $post_history = unserialize(file_get_contents(STORAGE_LOCATION."nodb.hist"));
        //Delete the selected post from the history
        if( isset($array[$post_id]) || array_key_exists($post_id, $post_history)){
            unset($post_history[$post_id]);
        }
        else{
            throw new \Exception("The post you are trying to remove from the post history could not be found.");
        }
        //Rewrite the history to disk
        file_put_contents(STORAGE_LOCATION."nodb.hist", serialize($post_history));
    }
}
