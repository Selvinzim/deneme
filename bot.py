dan  json  ithalat  dökümü , yük

dan  telgraf  ithalat  ParseMode , Güncellemesi

dan  telgrafı . Hata  içe aktarma  BadRequest

dan  telgrafı . ext  import  CallbackContext , Filters , MessageHandler , Updater

dan  lib  ithalat  get_chatid_usersid , get_client

config  =  yükle ( aç ( "config.json" ))

chatid_usersid : dict [ str , list [ int ]] =  load ( open ( "chatid_usersid.json" ) )

def  tag_user ( kullanıcı , parse_mode : str  =  ParseMode . MARKDOWN ) ->  str :

    if  parse_mode  ==  ParseMode . İŞARET :

        dönüş (

            f "[ { kullanım . first_name  veya  ' }  { kullanım . last_name  veya  ' } ] (tg: // kullanıcı kimliği = { kullanım . id } )"

        )

    if  parse_mode  ==  ParseMode . HTML :

        return  "<a href='tg://user?id= {kullanıcı. id}'> f { kullanıcı . first_name } </a>"

     NotImplementedError'ı yükseltin ( parse_mode  +  "desteklenmiyor!" )

def  tag_user_empty ( kullanıcı , parse_mode : str  =  ParseMode . MARKDOWN ) ->  str :

    if  parse_mode  ==  ParseMode . İŞARET :

        Dönüş  F "[ \ u200b ] (tg: // kullanıcı kimliği = { kullanım . id } )"

    if  parse_mode  ==  ParseMode . HTML :

        return  f "<a href='tg://user?id= {kullanıcı. id}'> \ u200b </a>"

     NotImplementedError'ı yükseltin ( parse_mode  +  "desteklenmiyor!" )

def  update_chatid_usersid ( chat_id : int , link : str ):

    istemci  =  get_client ( yapılandırma )

    usersid  =  get_chatid_usersid ( istemci , [ bağlantı ])[ chat_id ]

    chatid_usersid [ str ( chat_id )] = kullanıcı  kimliği

    dökümü ( chatid_usersid , open ( "chatid_usersid.json" , "w" ) )

def  bahsetme_all ( güncelleme : Güncelleme , bağlam : CallbackContext ) ->  Yok :

    eğer  değil  güncelleme . mesaj :

        dönüş

    eğer  herhangi ( filtreli ( lambda  x : x  de  güncelleme . mesajı . metin , yapılandırma [ "anahtar kelimeler" ])):

        sohbet  =  güncelleme . mesaj . sohbet etmek

        küresel  chatid_usersid

        eğer  str ( sohbet . id ) değil  de  chatid_usersid :

            dene :

                bağlantı  =  sohbet . export_invite_link ()

             BadRequest hariç :

                güncelleme . mesaj . cevap_metni (

                    "Kullanıcılar kaydedilmez! Lütfen botu yönetici olarak tanıtın ve ona 'Kullanıcıları bağlantı yoluyla davet et' ve 'Mesajları sil' izni verin!"

                )

                dönüş

            update_chatid_usersid ( sohbet . id , bağlantı )

        kullanıcılar  = []

         chatid_usersid [ str ( chat . id )] içindeki kullanıcı kimliği  için : 

            dene :

                kullanıcı  =  sohbet . get_member ( kullanıcı kimliği ). kullanıcı

                Kullanıcılar . ekle ( kullanıcı )

             BadRequest hariç :

                geçmek

        etiket_metin  =  ""

        için  kullanıcı  içinde  kullanıcılar :

            if  user  ==  güncelleme . mesaj . from_user :

                devam et

            tag_text  +=  tag_user_empty ( kullanıcı )

        dene :

            güncelleme . mesaj . sil ()

            bağlam . bot . send_message (

                sohbet . id ,

                metin = f" { tag_user ( güncelleme . mesaj . from_user ) } : { güncelleme . mesaj . metin } { tag_text } " ,

                parse_mode = ParseMode . İŞARETLEME ,

            )

         BadRequest hariç :

            güncelleme . mesaj . cevap_metni (

                f"通知了其他{ len ( kullanıcılar ) }個人！"  +  tag_text . şerit (),

                parse_mode = ParseMode . İŞARETLEME ,

            )

def  ana () ->  Yok :

    """Bot'u başlat."""

    c  =  get_client ( yapılandırma )

    c . bağlantıyı kes ()

    güncelleyici  =  Güncelleyici ( config [ "belirteç" ])

    gönderici  =  güncelleyici . sevk memuru

    sevk memuru . add_handler (

        MessageHandler (

            Filtreler . chat_type . gruplar  ve  Filtreler . metin  &  ~ Filtreler . komut , söz_hepsi

        )

    )

    güncelleyici . start_polling ()

    güncelleyici . boşta ()

if  __name__  ==  "__main__" :

    ana ()
