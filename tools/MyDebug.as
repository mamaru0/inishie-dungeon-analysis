package
{
   import flash.text.TextField;
   import flash.utils.*;
   
   public class MyDebug
   {
      
      public static var error_messages:Dictionary = new Dictionary();
      
      public static var Main:*;
       
      
      public function MyDebug()
      {
         super();
      }
      
      public function Set(key:String, value:int) : void
      {
         error_messages[key] = value;
      }
      
      public function ShowStacks(err:Error) : void
      {
         var text_field:TextField = new TextField();
         text_field.border = true;
         Main.addChild(text_field);
         text_field.x = 60;
         text_field.y = 60;
         text_field.width = 360;
         text_field.height = 240;
         var text:String = err.message + "\n";
         for(var k in error_messages)
         {
            var value:int = int(error_messages[k]);
            var key:String = String(k);
            text += key + ": " + value + "\n";
         }
         text_field.text = text;
      }
   }
}
