using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RealWines.NET.Models
{
    [Table("approval_queue")]
    public class ApprovalQueue
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("wine_id")]
        public int WineId { get; set; }

        [Column("submitted_by")]
        public string SubmittedBy { get; set; }

        [Column("submission_date")]
        public DateTime SubmissionDate { get; set; } = DateTime.UtcNow;

        [Column("status")]
        public string Status { get; set; } = "Pending";

        [Column("reviewed_by")]
        public string ReviewedBy { get; set; }

        [Column("review_date")]
        public DateTime? ReviewDate { get; set; }

        [Column("notes")]
        public string Notes { get; set; }

        public virtual Wine Wine { get; set; }
    }
}