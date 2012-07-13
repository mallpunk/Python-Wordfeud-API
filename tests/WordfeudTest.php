<?php
require __DIR__ .'/../Wordfeud.php';

class WordfeudTest extends PHPUnit_Framework_TestCase
{
    protected static $Wordfeud;

    protected static $userid;
    protected static $username;
    protected static $email;
    protected static $password;

    public static function setUpBeforeClass()
    {
        self::$Wordfeud     = new Wordfeud();

        self::$username     = 'TEST'. substr(md5(uniqid(true)), 0, 14);
        self::$email        = substr(md5(uniqid(true)), 0, 10) .'@test.com';
        self::$password     = substr(sha1(uniqid(true)), 0, 6);
    }

    public function testCreateAccount()
    {
        self::$userid = self::$Wordfeud->createAccount(
                            self::$username,
                            self::$email,
                            self::$password
                        );

        $this->assertTrue(is_numeric(self::$userid));
    }

    /**
     * @depends testCreateAccount
     */
    public function testSessionId() 
	{
        $this->assertNotSame(self::$Wordfeud->getSessionId(), NULL);
    }

    /**
     * @depends testSessionId
     */
    public function testLoginEmail() 
	{
        self::$Wordfeud->logInUsingEmail(self::$email, self::$password);
    }

    /**
     * @depends testSessionId
     */
    public function testLoginId() 
	{
        self::$Wordfeud->logInUsingId(self::$userid, self::$password);
    }

    /**
     * @depends testSessionId
     */
    public function testSearch() 
	{
        self::$Wordfeud->searchUser(self::$username);
    }

    // This test should always be the last one.
    public function testLogout() 
	{
        self::$Wordfeud->logOut();

        $this->assertSame(self::$Wordfeud->getSessionId(), NULL);
    }
}

