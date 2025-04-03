using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("varieties")]
    public class Variety
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("name")]
        [Required]
        public string Name { get; set; }

        public virtual ICollection<Wine> Wines { get; set; }
    }
}