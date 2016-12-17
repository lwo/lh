object Lineair {


  def main(args: Array[String]): Unit = {

    import java.io.File
    case class Config(file: File = new File("."), kwargs: Map[String,String] = Map())


    val parser = new scopt.OptionParser[Config]("scopt") {
      head("scopt", "3.x")

      opt[File]('f', "file").required().valueName("<file>").
        action( (x, c) => c.copy(file = x) ).
        text("file is a required file property")

      help("help").text("prints this usage text")
    }

    // parser.parse returns Option[C]
    parser.parse(args, Config()) match {
      case Some(config) =>
        config.file

      case None =>
      // arguments are bad, error message will have been displayed
    }

  }

}
